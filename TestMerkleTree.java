package functions;

import static org.apache.cassandra.utils.MerkleTree.RECOMMENDED_DEPTH;

import java.util.List;
import java.util.Map;
import java.util.TreeMap;

import org.apache.cassandra.dht.IPartitioner;
import org.apache.cassandra.dht.RandomPartitioner;
import org.apache.cassandra.dht.RandomPartitioner.BigIntegerToken;
import org.apache.cassandra.dht.Range;
import org.apache.cassandra.utils.MerkleTree;
import org.apache.cassandra.utils.MerkleTree.RowHash;
import org.apache.cassandra.utils.MerkleTree.TreeRange;
import org.apache.cassandra.utils.MerkleTree.TreeRangeIterator;

public class MerkleTreeTest { 

    public static void addRows(MerkleTree tree, Map<BigIntegerToken, byte[]> rows) { 
        MerkleTree.RowHash EMPTY_ROW = new MerkleTree.RowHash(null, new byte[0], (long) 0); 

        // Get the sub range iterator which iterates over sorted sub ranges 
        TreeRangeIterator ranges = tree.invalids(); 
        TreeRange range = ranges.next(); 

        for (BigIntegerToken token : rows.keySet()) { 
            while (!range.contains(token)) { 
                // add the empty hash, and move to the next range 
                range.addHash(EMPTY_ROW); 
                range = ranges.next(); 
            } 
            range.addHash(new RowHash(token, rows.get(token), (long) rows.size())); 
        } 
        if (range != null) { 
            range.addHash(EMPTY_ROW); 
        } 
        while (ranges.hasNext()) { 
            range = ranges.next(); 
            range.addHash(EMPTY_ROW); 
        } 
    } 

    public static void main(final String[] args) { 

        // Sorted map of hash values of rows 
        Map<BigIntegerToken, byte[]> rows1 = new TreeMap<BigIntegerToken, byte[]>(); 
        rows1.put(new BigIntegerToken("5"), new byte[] { (byte)0x09 }); 
        rows1.put(new BigIntegerToken("135"), new byte[] { (byte)0x0c }); 
        rows1.put(new BigIntegerToken("170"), new byte[] { (byte)0x05 }); 
        rows1.put(new BigIntegerToken("185"), new byte[] { (byte)0x02 }); 

        Map<BigIntegerToken, byte[]> rows2 = new TreeMap<BigIntegerToken, byte[]>(); 
        rows2.put(new BigIntegerToken("90"), new byte[] { (byte)0x03 }); 
        rows2.put(new BigIntegerToken("135"), new byte[] { (byte)0x0c }); 
        rows2.put(new BigIntegerToken("170"), new byte[] { (byte)0x05 }); 
        rows2.put(new BigIntegerToken("185"), new byte[] { (byte)0x02 }); 

        // Create Merkle tree of depth 3 for the token range (0 - 256] 
        IPartitioner partitioner = new RandomPartitioner(); 
        Range fullRange = new Range(new BigIntegerToken("0"), new BigIntegerToken("256")); 
        MerkleTree tree1 = new MerkleTree(partitioner, fullRange, RECOMMENDED_DEPTH, 8); 
        tree1.init(); 
        MerkleTree tree2 = new MerkleTree(partitioner, fullRange, RECOMMENDED_DEPTH, 8); 
        tree2.init(); 

        // Add row hashes 
        addRows(tree1, rows1); 
        addRows(tree2, rows2); 

        // Calculate hashes of non leaf nodes 
        List<TreeRange> diff = MerkleTree.difference(tree1, tree2); 
        System.out.println("tree1: " + tree1); 
        System.out.println("tree2: " + tree2); 
        System.out.println("difference: " + diff); 
    } 
}